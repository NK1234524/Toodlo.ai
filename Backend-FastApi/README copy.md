# Uv 
It is the modern tool used to manage both of the pip and vnev.It handles both packages and virtual enviroment.

Three commands which is used for Fast api:

(a) uv init
(b) uv add "fastapi[standard]"
(c) uv run fastapi dev

Don't always use async def you can also use def. Try to use async def when you need to extract data from the database.

# Enums
Enums are the concept i.e used to make the choices restricted so that only particular choice you are having and you have to select or fill from them only.

after enums to utilize that we need a pydantic class in which BaseModel is present and we have to use that enum into it further we need to use that Function of BaseModel in the get or post request.

# Query parameter and Path parameters

When we include the parameter in the path then we will consider it into the Path parameter.Whereas when we don't have any parameter in the path then we consider it into a query.

so if we are using a code like query here then it should be like this :
/items/?skip=value limit=value

***HERE IS THE CONCEPT***

skip = from where to start  &  limit = from where to end or upto where to end.
Pagination is included here. In query is the key-value pairs that go after ? in a URL seperated by & characters.

One small thing to understand next: limit is not controlling the database itself. It's simply a value coming from the URL that your Python code uses to decide how many todos to return.

Query parameter = extra information sent through the URL to control/filter what the endpoint returns.s

# Query Parameter with string validation
Annotated[str | None,Query(validation)]=None
*Advantages of Annotated*
Using Annotated is recommended instead of the default value in function parameters, it is better for multiple reasons. 🤓

The default value of the function parameter is the actual default value, that's more intuitive with Python in general. 😌

You could call that same function in other places without FastAPI, and it would work as expected. If there's a required parameter (without a default value), your editor will let you know with an error, Python will also complain if you run it without passing the required parameter.

When you don't use Annotated and instead use the (old) default value style, if you call that function without FastAPI in other places, you have to remember to pass the arguments to the function for it to work correctly, otherwise the values will be different from what you expect (e.g. QueryInfo or something similar instead of str). And your editor won't complain, and Python won't complain running that function, only when the operations inside error out.

Because Annotated can have more than one metadata annotation, you could now even use the same function with other tools.

*Query Parameter also includes a feature of regular expression*
i.e 

# Query parameter list/Multiple values
To declare a query parameter with a type of list, like in the example above, you need to explicitly use Query, otherwise it would be interpreted as a request body.

Annotated[List[str] | None,Query()]= None

We can also use default list value 
Annotated[List[str],Query()]= ['foo','me']
Without the str or any data type we can also use list but the concept which is important here is then list contents cannot be identifiable with particular data and it type.

