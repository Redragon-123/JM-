def content_edit(all_data):
    select_category = input("Please select a catogory from shopping, work and personal： ").lower().strip()
    #all_data[select_category] is a list of dicts
    for task in all_data[select_category]:
        print(f"work number: {task["work_number"]} \nwork description: {task["work_description"]}")
    
    select_task = input("Please enter the work number of the work you want to edit: ")
    #task is a dict containing work_number, work_description, work_priority, work_deadline
    for task in all_data[select_category]:
        if task["work_number"] == select_task:
            while True:
                print(f"You have selected the task: {task["work_number"]} \n{task["work_description"]} \n{task["work_priority"]} \n{task["work_deadline"]}")
                edit_part = input("Please enter the part you want to edit (work_deadline/work_description/work_priority): ").lower().strip()
                if edit_part in task["work_number"]:
                    new_value = input(f"Please enter the new value for {edit_part}: ")

                    task["work_number"][edit_part] = new_value
                    print("Task updated successfully.")
                    print(f"You have changed the task: {task["work_number"]} \n{task["work_description"]} \n{task["work_priority"]} \n{task["work_deadline"]}")
                    return all_data
                else:
                    print("Invalid part selected.Please try again.")
    
    print("Invalid work number, please try again.")
    return 