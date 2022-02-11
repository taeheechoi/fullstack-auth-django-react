1. Quality Software Development

Does software complies with or meet design based on functional requirements and specifications? Correct Software

Does software meets no-function requirements such as robustness and maintainability? Needed

Measurements: Code-based analysis, Reliability, Efficiency, Security, Maintainability, Size 
```
https://en.wikipedia.org/wiki/Software_quality
Reliability
Avoid software patterns that will lead to unexpected behavior (Uninitialized variable, null pointers, etc.)
Methods, procedures and functions doing Insert, Update, Delete, Create Table or Select must include error management
Multi-thread functions should be made thread safe, for instance servlets or struts action classes must not have instance/non-final static fields

Efficiency
Ensure centralization of client requests (incoming and data) to reduce network traffic
Avoid SQL queries that don't use an index against large tables in a loop

Security
Avoid fields in servlet classes that are not final static
Avoid data access without including error management
Check control return codes and implement error handling mechanisms
Ensure input validation to avoid cross-site scripting flaws or SQL injections flaws

Maintainability
Deep inheritance trees and nesting should be avoided to improve comprehensibility
Modules should be loosely coupled (fanout, intermediaries) to avoid propagation of modifications
Enforce homogeneous naming conventions

```

2. Tools/Frameworks
```
Fullstack
    Frontend
        Libraries:
        1. Material UI
        2. React-Bootstrap
        3. React Router
        4. Semantic UI
        5. Elastic UI
        6. Redux, Redux Toolkit - For complex state management
        7. NextJS
        8. React cookies
        9. Vue

    Backend
        Libraries:
        1. Django
        2. Django Rest Framework
        3. Django Filter
        4. Django Simple JWT
        5. Django CORS Headers
        6. Flask
        7. Celery
        8. Django Cron
        9. Django extensions
        10. Django crispy forms
        11. Django Haystack

    Python project
        Tensorflow

# .Net
    1. .Net - Epicor
    2. Infragistics - UI tool

### IDE
    1. VSCode
    2. Visual Studio
    3. SQL Management Tool
    4. Android Studio




```

