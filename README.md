from favro import Favro

fvr = Favro('favro_user@email', u'favro_user_API_token', u'favro_organization_id')

collections = favro.collections.getCollections()
https://favro.com/developer/#get-all-collections

collection = favro.collections.getCollectionByName("collection name")
https://favro.com/developer/#get-a-collection

collection_widgets = collection.getWidgets()
https://favro.com/developer/#get-all-widgets

widget = collection_widgets[2]
https://favro.com/developer/#get-a-widget

widget_columns = widget.getColumns()
https://favro.com/developer/#get-all-columns

column = widget_columns[0]
https://favro.com/developer/#get-a-column

column_cards = column.getCards()
https://favro.com/developer/#get-all-cards

card = column_cards[0]
https://favro.com/developer/#get-a-card

card_taskLists = card.getTaskLists()
https://favro.com/developer/#get-all-tasklists

tasklist = card_taskLists[0]
https://favro.com/developer/#get-a-task-list

tasks = card.getTasks(tasklist)
card is a required argument for getting tasks list, and tasklist is an optional filter. https://favro.com/developer/#tasks

tasklist.createTask("task name")
https://favro.com/developer/#create-a-task

new_tasklist = card.createTaskList("new tasklist", position=1, tasks=[{'name': 'test task 1', 'completed': False}, {'name': 'test task 2'}])
Request returned code 400: Bad Request: Unexpected value of position
Request returned code 400: Bad Request: Unexpected value of tasks
workaround:
tasklist = card.createTaskList("tasklist name")
tasks_list = [
    u'task1 name',
    u'task2 name',
    u'task3 name',
    u'task4 name'
]
for task in tasks_list:
    tasklist.createTask(task)
