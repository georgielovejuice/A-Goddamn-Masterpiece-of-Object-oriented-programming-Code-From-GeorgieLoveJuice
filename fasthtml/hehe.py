from fasthtml.common import *
from Log import Log
from Calculator import Calculator

app,rt = fast_app()

log = Log()
calc = Calculator(log)


@rt("/")
def get():

   return Titled("MyCalculator",
        Div( Form(
            Input(type="text", id="a", name="a", value="1"),
            Input(type="text", id="b", name="b", value="1"),
            P(f"Result = ", id="count"),
            Button("Add",hx_post="/add", hx_target="#count", hx_swap="innerHTML"),
            Button("Subtract",hx_post="/subtract", hx_target="#count", hx_swap="innerHTML"),
            Button("Multiply",hx_post="/multiply", hx_target="#count", hx_swap="innerHTML"),
            Button("Division",hx_post="/div", hx_target="#count", hx_swap="innerHTML")
        )),
        Div( Form(
           Button("show log",hx_get="/showlog", target_id="log_rows") ,
           Table(
            Thead(Tr(Th("log detail"))),
            Tbody(Tr(Td("None")),id = "log_rows")
            )
        )
        )
   )


@dataclass
class Dat: a:str;b:str

@rt('/add')
def post(dat:Dat):
    a = int(dat.a)
    b = int(dat.b)
    return f"{a} + {b} = {calc.add(a,b)}"

@rt('/subtract')
def post(dat:Dat):
    a = int(dat.a)
    b = int(dat.b)
    return f"{a} + {b} = {calc.subtract(a,b)}"

@rt('/multiply')
def post(dat:Dat):
    a = int(dat.a)
    b = int(dat.b)
    return f"{a} + {b} = {calc.multiply(a,b)}"

@rt('/div')
def post(add:Dat):
    a = int(add.a)
    b = int(add.b)
    return f"{a} + {b} = {calc.division(a,b)}"

@rt('/showlog')
def get():
        return Tbody(*[Tr(Td(i),Td(Button("delete", hx_get=f"/delete_log/{idx}", target_id="log_rows")),id=f"log-{idx}") for idx,i in enumerate(calc.show_log())])

#    return Table(
#            Thead("log detail"),
#            Tbody(*[Tr(Td(i),Td(Button("delete", hx_get=f"/delete_log/{idx}", target_id="log_rows")),id=f"log-{idx}") for idx,i in enumerate(calc.show_log())]),
#            id='log_table'
#        )

@rt('/delete_log/{id}')
def get(id:int):
    calc.delete_log(id)
    return Tbody(*[Tr(Td(i),Td(Button("delete", hx_get=f"/delete_log/{idx}", target_id="log_rows")),id=f"log-{idx}") for idx,i in enumerate(calc.show_log())])
#    return Table(
#            Thead("log detail"),
#            Tbody(*[Tr(Td(i),Td(Button("delete", hx_get=f"/delete_log/{idx}", target_id="log_rows")),id=f"log-{idx}") for idx,i in enumerate(calc.show_log())]),
#            id='log_table'
#        )


serve()