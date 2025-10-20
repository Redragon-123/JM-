def search_dict(dict_name, keyword, search_mode="all", case_sensitive=False):
    results = {}
    keyword = keyword.lower() 
    def check_and_collect(current_dict):
        has_match = False
        for key, value in current_dict.items():
            key_str = str(key)
            if not case_sensitive:
                key_str = key_str.lower()
            if keyword in key_str:
                has_match = True
            value_str = str(value)
            if not case_sensitive:
                value_str = value_str.lower()
            if keyword in value_str:
                has_match = True
            if isinstance(value, dict):
                check_and_collect(value)
            if has_match and current_dict not in results:
                results.append(current_dict)
    check_and_collect(dict_name)
    return results





dict_name = {}
while True:
    keyword = input("What do you want to search?: ").strip()
    if not keyword:
        print("Please enter a valid keyword.")
        continue
    if keyword.lower() == "exit":
        print("Exiting the search.")
        break
    results = search_dict(dict_name=dict_name, keyword=keyword, search_mode="all", case_sensitive=False)
    print("Search completed. Results:")
    if results:
        for res in results:
            print(res)
        else:   
            print("No matches found.")