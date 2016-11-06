import { Meteor } from 'meteor/meteor';
import React from 'react';
import { render } from 'react-dom';
import { Router, Route, browserHistory } from 'react-router';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { createStore } from 'redux';
import { Provider } from 'react-redux';

import App from '../../ui/App.jsx';
import reducers from '../../ui/redux/reducers';

const store = createStore(reducers);

Meteor.startup(() => {
  render(
    <Provider store={store}>
      <MuiThemeProvider>
        <Router history={browserHistory}>
          <Route path="/" component={App} />
        </Router>
      </MuiThemeProvider>
    </Provider>,
    document.getElementById('render-target')
  );
});
