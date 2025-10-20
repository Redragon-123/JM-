'''
The task is to create a to-do list application

Specification:
You should design an appropriate data structure for the to-do list.
You should use functions where appropriate.
You should create an appropriate programming structure to "drive" the application.

Good programming practice:
Functions should have one purpose (single responsibility principle).
Meaningful names for variables and functions.
Document your functions.
'''
def edit_file():
    categories = {'work':[],'personal':[],'shopping':[]}
    choose_key=input('what categories do you want to edit? (work/personal/shopping): ').lower()
    if choose_key=='work':
        function= input('what do you want to do? (add/remove): ').lower()
        if function=='add':
            work_priority=input('please enter the priority of the task you want to add(AAA/AA/A/B/C): ').upper()
            work_deadline=input('please enter the deadline of the task you want to add (DD/MM/YYYY): ')
            work_desciption=input('please enter the description of the task you want to add: ')
            work_number = len(categories[choose_key]) + 1
            task= f'ID:{work_number:04d},Priority: {work_priority}, Deadline: {work_deadline}, Description: {work_desciption}'
            categories['work'].append(task)
            print(f'"{task}" added to work list.')
        elif function=='remove':
            print('Current work tasks:')
            for x in categories['work']():
                print(f"{x}['id']")
            target_id=input('please enter the ID of the task you want to remove: ')
            found = False
            for i, task in enumerate(categories['work']):
                if task['id'] == target_id:
                    removed_task = categories['work'].pop(i)
                    print(f"✓ remove work have done: {removed_task['id']} - {removed_task['description']}")
                    found = True
                    break
                if not found:
                    print(f"✗ {target_id} not found in work tasks.")
    elif choose_key=='personal':
        function= input('what do you want to do? (add/remove): ').lower()
        if function=='add':
            personal_priority=input('please enter the priority of the task you want to add(AAA/AA/A/B/C): ').upper()
            personal_deadline=input('please enter the deadline of the task you want to add (DD/MM/YYYY): ')
            personal_desciption=input('please enter the description of the task you want to add: ')
            personal_number = len(categories[choose_key]) + 1
            task= f'ID:{personal_number:04d},Priority: {personal_priority}, Deadline: {personal_deadline}, Description: {personal_desciption}'
            categories['personal'].append(task)
            print(f'"{task}" added to personal list.')
        elif function=='remove':
            print('Current personal tasks:')
            for x in categories['personal']():
                print(f"{x}['id']")
            target_id=input('please enter the ID of the task you want to remove: ')
            found = False
            for i, task in enumerate(categories['personal']):
                if task['id'] == target_id:
                    removed_task = categories['personal'].pop(i)
                    print(f"✓ remove personal have done: {removed_task['id']} - {removed_task['description']}")
                    found = True
                    break
                if not found:
                    print(f"✗ {target_id} not found in personal tasks.")
    elif choose_key=='shopping':
        function= input('what do you want to do? (add/remove): ').lower()
        if function=='add':
            shopping_priority=input('please enter the priority of the task you want to add(AAA/AA/A/B/C): ').upper()
            shopping_deadline=input('please enter the deadline of the task you want to add (DD/MM/YYYY): ')
            shopping_desciption=input('please enter the description of the task you want to add: ')
            shopping_number = len(categories[choose_key]) + 1
            task= f'ID:{shopping_number:04d},Priority: {shopping_priority}, Deadline: {shopping_deadline}, Description: {shopping_desciption}'
            categories['shopping'].append(task)
            print(f'"{task}" added to shopping list.')
        elif function=='remove':
            print('Current shopping tasks:')
            for x in categories['shopping']():
                print(f"{x}['id']")
            target_id=input('please enter the ID of the task you want to remove: ')
            found = False
            for i, task in enumerate(categories['shopping']):
                if task['id'] == target_id:
                    removed_task = categories['shopping'].pop(i)
                    print(f"✓ remove shopping have done: {removed_task['id']} - {removed_task['description']}")
                    found = True
                    break
                if not found:
                    print(f"✗ {target_id} not found in shopping tasks.")
      
        
            





