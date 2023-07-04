class SearchDataStructure:
    def __init__(self, title, search_list, email, town):
        self.title = title
        self.search_list = search_list
        self.email = email
        self.town = town

    def add_keyword(self, keyword):
        if keyword not in self.search_list:
            self.search_list.append(keyword)

    def delete_keyword(self, keyword):
        if keyword in self.search_list:
            self.search_list.remove(keyword)
        else:
            print(f"The keyword '{keyword}' does not exist in the list.")

    def get_list(self):
        return self.search_list

    def change_title(self, new_title):
        self.title = new_title