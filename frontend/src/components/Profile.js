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
const theme = createTheme()

const Profile = () => {
    let navigate = useNavigate()

    const [cookies, setCookies] = useCookies(['user'])

    const handleSubmit = (e) => {
        e.preventDefault()
        const data = new FormData(e.currentTarget);
        // eslint-disable-next-line no-console
        // console.log({
        //   email: data.get('email'),
        //   password: data.get('password'),
        // });

        axios.post(`http://127.0.0.1:8000/auth/login/`, {
            username: data.get('username'),
            password: data.get('password')
        })
            .then(res => {
                // console.log(res);
                // console.log(res.data);
                setCookies('access', res.data.access, { path: '/' }) //# path:'/' signifies that the cookie is available for all the pages of the website
                setCookies('refresh', res.data.refresh, { path: '/' })
                navigate('/profile')

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
                        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="username"
                                label="Username"
                                name="username"
                                autoComplete="username"
                                autoFocus
                            />
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="firstName"
                                name="firstName"
                                label="First Name"

                            />
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="lastName"
                                name="lastName"
                                label="Last Name"
                            />
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="email"
                                label="Email Address"
                                name="email"
                                autoComplete="email"
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
                    </Box>
                    <Copyright sx={{ mt: 8, mb: 4 }} />
                </Container>
            </ThemeProvider>
        </div>
    )
};

export default Profile;
