import React from 'react';
import AppBar from 'material-ui/AppBar';
// import { createContainer } from 'meteor/react-meteor-data'

// import Shows from '../api/shows.js';
import MDLInputView from './components/MDLInputView.jsx';
import MDLShowsList from './components/MDLShowsList.jsx';
import MDLTopShows from './components/MDLTopShows.jsx';

const App = () => (
  <div>
    <AppBar
      title="MDL Recs"
      showMenuIconButton={false}
    />
    <MDLInputView />
    <MDLShowsList />
    <MDLTopShows />
  </div>
);

export default App;
