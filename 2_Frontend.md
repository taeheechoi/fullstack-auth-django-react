

1. Redirect
```js
import {Redirect} from 'react-router'
export default class Test extends Component {
    render() {
        if(this.state.isLoggedIn){
            return <Redirect to="/loggedin" />
        } 
    }
}

export default Test = () => {
    render() {
        if(loggedIn){
            <Redirect to="/loggedin" />
        }
    }
}
```

2. pass data between sibling components
```js
export default class Test extends Component {
    render(){
        return(
            <Router>
                <Route path="test/:testId" component={SecondPage} />
                <Route path="/" component={FirstPage}/>
            </Router>
        )
    }
}

export default FirstPage = (props) => {
    const handleClick = (data) => {
        props.history.push(`/test/${data}`)
    }
    return(
        <>
            <button onClick={() => handleClick('FromFirstPage')}> Click </button>
        </>
    )
}

export default SecondPage = (props) => {
    if(!props.match.params.testId){
        return <div> No data </div>
    }
    return (
        <div>${props.match.params.testId}</div>
    )
}
```

3. Browser Resize 

https://www.interviewbit.com/react-interview-questions/#how-to-re-render-the-view-when-the-browser-is-resized

4. Switching Pages

https://www.interviewbit.com/react-interview-questions/#how-to-create-a-switching-component-for-displaying-different-pages

5. 
npm: install packages in the a project

npx: running commands on Node

JSX will permit you for writing HTML-style template syntax 

6. Conditional rendering, if-else, ternary operation, using let element variables

7. React router, for routing, building a single-page web application without refreshing page

8. Performance class vs hook, hook avoids a lot of overheads(instance creation, binding, etc), smaller component tree, render props less work

9. Hooks: useState, useEffect, useContext, useRef, useMemo, useReducer, useCallback, useWhatever

https://www.interviewbit.com/react-interview-questions/#explain-about-types-of-hooks

10. Lifecycle, constructor(), getDerivedStateFromPrpos(), render(), componentDidMount(), shouldComponentUpdate(), getSnapshotBeforeUpdate(), componentDidUpdate(), componentWillUnmount()

11. HOC, DRY

https://www.interviewbit.com/react-interview-questions/#what-are-higher-order-components

12. props, child -> parent
```js
export default Parent = () => {
    const [counter, setCounter] = useState(0)

    let increment = value => setCounter(++counter)
    return(
        <>
            <Child increment={increment} counter={counter}>
        </>
    )
}

export default Child = ({increment, counter}) => {
    return(
        <>
            <button onClick={() => increment(++counter)}>/>
        </>
    )
}

```
13. Optimization: useMemo, state collocation, lazy loading, purcomponent(reduce re-renders)

14. Styling, Inline Styling, JS object, CSS style, css Module(.module.css)

15. Prevent re-rendering on Class. Use shouldComponentUpdate() -> return false on Child component

https://www.interviewbit.com/react-interview-questions/#how-to-prevent-re-renders

16. StrickMode, check components with unsafe lifecycle, warning legacy string refs instead of callback ref, warning on findDOMNode, warning on legacy context API 

17. React hook rules, must be called at the top level (not allowed in the nested function, loops or condition), callable from function components only

18. Error boundaries, with it blank page, 

https://www.interviewbit.com/react-interview-questions/#what-are-error-boundaries

19. Type of side effects, side effect without clean up(useEffect, network request, logging, DOM mutation), side effect with cleanup (some hook effect required due to memory leak, data source subscription)

20. Controlled vs Uncontrolled components, controlled by React or DOM itself(no perform any actions in React)
```js
controlled:
const FormValidation = (props) => {
    const [input, setInput] = useState('')
    const updateInput = (e) => {setInput(e.target.value)}
    return(
        <>
            <form>
                <input type="text" value={input} onChange={updateInput} />
            </form>
        </>
    )
}

uncontrolled:
const FormValidation = (props) => {
    let input = useRef(null)
    const handleSubmit = (e) => {
        alert(`Input: ${input.current.value}`)
        e.preventDefault()
    }
    return (
        <>
            <form onSubmit={handleSubmit}>
                <input type="text" ref={input}>
                <button type="submit"> Submit </button>
            </form>
        </>
    )
}


```


### References

https://www.interviewbit.com/react-interview-questions/#