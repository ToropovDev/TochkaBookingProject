import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Login from './components/Login.jsx';
import InputToken from './components/InputToken.jsx';
import Games from './components/Games.jsx';
import GameDetails from './components/GameDetails.jsx';
import Profile from './components/Profile.jsx';
import UserProfile from "./components/UserProfile.jsx";
import MyTeams from "./components/MyTeams.jsx";
import MyGames from "./components/MyGames.jsx";

const AppRouter = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/input-token" element={<InputToken/>}/>
                <Route path="/games" element={<Games/>}/>
                <Route path="/profile" element={<Profile/>}/>
                <Route path="/my-teams" element={<MyTeams />} />
                <Route path="/my-games" element={<MyGames />} />
                <Route path="/users/:userId" element={<UserProfile/>}/>
                <Route path="/games/:gameId" component={GameDetails}/>

                <Route path="*" element={<div>404</div>}/>
            </Routes>
        </Router>
    );
};

export default AppRouter;