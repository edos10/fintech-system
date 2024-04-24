## Объяснение выбранного сценария и аргументация выбора:
_______

Поскольку в PE мы храним кредитные договора, а до этого нужно
одобрение заявки, чтобы договор был создан, поэтому все
заявки, которые когда-либо были отправлены, будем хранить в БД сервиса Origination.
На мой взгляд, сервису Origination нужна своя БД, а Scoring тогда
просто будет ходить в PE и проверять клиента.

С API просто запрос будет идти в Origination, а там будет проверяться,
продублирована ли заявка или нет, а затем проверяем все в Scoring.

На мой взгляд, довольно логично иметь прослойку в виде
Origination для обработки заявок, чтобы создавать из них
кредитные договора, если это возможно. Поэтому последовательность
взаимодействия сервисов такова.

И еще, кажется, полезно хранить все совершенные заявки клиентов,
даже те, которые отменились или было отказано, думаю, что сотрудникам
может пригодиться эта информация.

Что касается отказа какого-либо сервиса в процессе обработки заявки,
давайте рассмотрим различные случаи:

1) **Отказ Origination**: здесь просто клиенту придется отправить
заявку еще раз, когда сервис оживет
2) **Отказ Scoring**: здесь проверка клиента упадет, однако заявка уже внесется в БД,
кажется, проще ее удалить из БД, потому что она в непонятном состоянии,
поэтому в зависимости от запроса в Scoring делаем соответствующие
изменения в Origination
3) **Отказ Product Engine**: если это запрос от Scoring, то идем в кейс Scoring,
если это POST /agreement, то придется также удалить и заявку на кредит в Origination,
если не удалось создать кредитный договор по одобренной заявке.

И в этих случаях тогда система будет возвращаться в согласованное состояние.


## **Джобы в Origination**:
1) **applications_to_scoring**

Ее роль заключается в том, чтобы все заявки со статусом new отправлять в scoring и ставить статус "scoring", пока они на проверке в Scoring. Джобу можно запускать в зависимости от параметра в конфиге config.py, по умолчанию я выставил 30 секунд, чтобы сильно не нагружать систему и при этом был +- адекватный отклик для пользователя, хотя можно уменьшить и до 15-20 секунд, главное - не делать каждую секунду, это может существенно увеличить нагрузку на сервис. 

За один подход собираются все заявки со статусом "new" и отправляются в scoring, если scoring ответит с кодом 200, значит, он принял заявки и мы можем в origination поменять статусы этих заявок на "scoring", так будет согласованное состояние системы.

2) **accepted_applications_to_pe**

Ее роль в том, чтобы все заявки с accepted статусом порождали договора на кредит в PE, то есть по каждой одобренной заявке на кредит идем в PE и явно создаем договор :) ну и потом прописываем agreement_id в БД Origination, чтобы знать, какой у нас кредитный договор на эту заявку.