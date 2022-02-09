import React, { useState, useEffect } from 'react';
import { DataGrid, GridToolbar  } from '@mui/x-data-grid';
import axios from 'axios';
import { useCookies } from 'react-cookie';

const Todo = () => {
    const [todoList, setTodoList] = useState([])
    
    const [cookies, setCookies] = useCookies(['user'])


    useEffect(() => {
        const getTodoData = async () => {
            const result = await axios.get(`http://127.0.0.1:8000/todo/`, { headers: { "Authorization": `Bearer ${cookies.access}` } })
            console.log(result)
            setTodoList(result.data)
        }
        getTodoData()
    }, [])

    console.log(todoList)

    const columns = [
        {field: 'title', headerName: 'Title', width:100, editable: true},
        {field: 'description', headerName: 'Description', editable: true},
        {field: 'isComplete', headerName: 'Complete',  type: 'boolean', editable: true}

    ]

    const rows = todoList.map((todo) => ({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'isComplete': todo.is_complete           
    }))
  
    return (
        <div style={{height:500, margin: 10}}>
            <DataGrid rows={rows} columns={columns} components={{Toolbar: GridToolbar}} />
        </div>


  );
};

export default Todo;
