def content_edit(all_data):
    select_category = input("Please select a catogory from shopping, work and personal： ").lower().strip()
    for task in all_data[select_category]:
        print(f"work number: {task["work_number"]} \nwork description: {task["work_description"]}")
    
    select_task = input("Please enter the work number of the work you want to edit: ")
    