import React from 'react';
import AppBar from 'material-ui/AppBar';
import Grid from 'material-ui/Grid';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';

import MDLInputView from './components/MDLInputView.jsx';
import ShowList from './components/ShowList.jsx';
import HighlightList from './components/HighlightList.jsx';

class App extends React.Component {
  render() {
    return (
        <div>
          <AppBar position={'static'}>
            <Toolbar>
              <Typography type={'title'} color={'inherit'}>
                MDL Recs
              </Typography>
            </Toolbar>
          </AppBar>
          <Grid container>
            <Grid item xs={12} md={3}>
              <MDLInputView/>
              <ShowList/>
            </Grid>
            <Grid item xs={12} md={9}>
              <HighlightList/>
            </Grid>
          </Grid>
        </div>
    );
  }
}

export default App;
