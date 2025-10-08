from retail_project.connectors.employee_connector import EmployeeConnector

ec=EmployeeConnector()
ec.connect()
em=ec.login("putin@gmail.com","123")
if em==None:
    print("login fail")
else:
    print("login success")
    print(em)