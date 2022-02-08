import {
    Avatar,
    Box,
    Button,
    Container,
    createTheme,
    CssBaseline,
    Link,
    TextField,
    ThemeProvider,
    Typography
} from '@mui/material';

import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import axios from 'axios';
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

const Copyright = (props) => {
    return (
        <Typography variant="body2" color="text.secondary" align="center" {...props}>
            {"Copyright ©"}
            <Link color="inherit" href="#">
                Tae Hee Choi
            </Link>{' '}
            {new Date().getFullYear()}
            {"."}
        </Typography>
    )

}

const MyTextField = (props) => {
    return <TextField value={props.value}  {...props} />
}

const theme = createTheme()

const Profile = () => {
    let navigate = useNavigate()
    const [user, setUser] = useState([])
    const [cookies, setCookies] = useCookies(['user'])


    useEffect(() => {
        const userData = async () => {
            const result = await axios.get(`http://127.0.0.1:8000/auth/user_detail/`, { headers: { "Authorization": `Bearer ${cookies.access}` } })
            setUser(result.data)
        }
        userData()
    }, [])

    const handleSubmit = (e) => {
        e.preventDefault()
        const data = new FormData(e.currentTarget);
        // eslint-disable-next-line no-console
        // console.log({
        //   email: data.get('email'),
        //   password: data.get('password'),
        // });

        axios.put(`http://127.0.0.1:8000/auth/user_detail/`, {
            username: data.get('username'),
            first_name: data.get('firstName'),
            last_name: data.get('lastName'),
            email: data.get('email'),
            
        }, { headers: { "Authorization": `Bearer ${cookies.access}` } })
            .then(res => {
                console.log(res);
                console.log(res.data);

            })

    }
    return (
        <div>
            <ThemeProvider theme={theme}>
                <Container component="main" maxWidth="xs">
                    <CssBaseline />
                    <Box
                        sx={{
                            marginTop: 8,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center'
                        }}
                    >
                        <Avatar sx={{ m: 1, bgcolor: 'primary.main' }}>
                            <ManageAccountsIcon />
                        </Avatar>
                        <Typography component="h1" variant="h5">
                            Profile
                        </Typography>
                        {user.map((usr) => (
                             <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                             <MyTextField
                                 margin="normal"
                                 required
                                 fullWidth
                                 id="username"
                                 label="Username"
                                 name="username"
                                 value={usr.username}
                             />

                             <TextField
                                 margin="normal"
                                 required
                                 fullWidth
                                 id="firstName"
                                 name="firstName"
                                 label="First Name"
                                 value={usr.first_name}
                             />
                             <TextField
                                 margin="normal"
                                 required
                                 fullWidth
                                 id="lastName"
                                 name="lastName"
                                 label="Last Name"
                                 value={usr.last_name}
                             />
                             <TextField
                                 margin="normal"
                                 required
                                 fullWidth
                                 id="email"
                                 label="Email Address"
                                 name="email"
                                 value={usr.email}
                             />

                             <Button
                                 type="submit"
                                 fullWidth
                                 variant="contained"
                                 sx={{ mt: 3, mb: 2 }}
                             >
                                 Update Profile
                             </Button>
                         </Box>


                        ))}
                           
                  
                    </Box>
                    <Copyright sx={{ mt: 8, mb: 4 }} />
                </Container>
            </ThemeProvider>
        </div>
    )
};

export default Profile;
