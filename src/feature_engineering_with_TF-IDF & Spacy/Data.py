import pandas as pd

class Data:
    def __init__(self, initial_rows=0):
        self.col_document_name ="document_name"
        self.col_student_ID = "student_ID"
        self.col_document_vector = "document_vector"
        self.col_decision = "decision"
        self.data = pd.DataFrame(
            columns=[self.col_document_name, self.col_document_vector, self.col_decision, self.col_student_ID],
            index=range(initial_rows)
        )

    def add_data(self, document_name,document_vector, decision,student_ID=""):
        new_row = {
            "document_name": document_name,
            "student_ID": student_ID,
            "document_vector": document_vector,
            "decision": decision
        }
        self.data = self.data._append(new_row, ignore_index=True)
        return self.data
    
    def get_vector(self, document_name):
        row = self.data[self.data["document_name"] == document_name].iloc[0]
        return row["document_vector"]
    
    def get_decision(self, document_name):
        row = self.data[self.data["document_name"] == document_name].iloc[0]
        return row["decision"]
    
    def get_student_ID(self, document_name):
        row = self.data[self.data["document_name"] == document_name].iloc[0]
        return row["student_ID"]
       
    def get_row(self, document_name):
        row = self.data[self.data["document_name"] == document_name].iloc[0]
        return row
    
    def remove_row(self, document_name):
        self.data = self.data[self.data["document_name"] != document_name]
    
    def get_data(self):
        return self.data
    
    def save_to_csv(self, filepath):
        self.data.to_csv(filepath, index=False)

    def load_from_csv(self, filepath):
        obj = Data()  
        obj.data = pd.read_csv(filepath)
        return obj

if __name__ == "__main__":
    data_obj= Data()
    print("Example of adding data to the data object")
    data_obj.add_data("a.txt", [1,2,3], 2, "52-14173")
    data_obj.add_data("e.txt", [11,22,8], 1, "49-5151")
    data_obj.add_data("i.txt", [15,68], 0)
    print(data_obj.get_data())
    print(data_obj.get_vector("a.txt"))
    print(data_obj.get_decision("a.txt"))
    print(data_obj.get_student_ID("a.txt"))
    print(data_obj.remove_row("a.txt"))
    print(data_obj.get_row("e.txt")[data_obj.col_document_vector])
    print(data_obj.get_data())