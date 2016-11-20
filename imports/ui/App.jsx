import React from 'react';
import AppBar from 'material-ui/AppBar';
import Paper from 'material-ui/Paper';
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
    <Paper style={{ padding: 10 }} zDepth={2}>
      <h3>Project Outline</h3>
      <p><b>Goal:</b> Create a product that helps watchers find interesting
      upcoming, airing, finished shows.</p>

      <b>Market:</b> Young adults, mostly girls, familiar with MDL
        <ul>
          <li>Design is important</li>
          <li>Deep product simple w/ intuitive one-way flow</li>
        </ul>

      <p><b>Marketing:</b> A post on MDL forum</p>

      <p><b>Product:</b> A simple, quick-loading dashboard.</p>
      <ol>
        <li>User logs in</li>
        <li>Dta entered into a predictive model</li>
        <li>Returns recommended movies, shows, and similar users.</li>
      </ol>

      <p><b>Tech Stack:</b> Meteor app with MongoDB database, React, Material-UI</p>

      <b>Basic user experience:</b>

      <ol>
        <li>User logs in.</li>
        <li>HTTP GET http://mydramalist.com/dramalist/USERNAME</li>
        <li>Parse HTML to get a table of shows.</li>
        <li>Send the list of show objects to the model.</li>
        <li>Model computes a preference vector for the user.</li>
        <li>Display 5 shows, 5 movies, and 5 similar users.</li>
      </ol>

      <b>Creating the model:</b>
      <ol>
        <li>Use a web scraper to get drama lists of users that
        frequent the forums.</li>
        <li>Transform data into correct format</li>
        <li>Train model.</li>
        <li>????</li>
        <li>Trained model with data.</li>
      </ol>
    </Paper>
  </div>
);

export default App;
