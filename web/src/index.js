import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route} from 'react-router-dom';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import {createStore} from 'redux';
import {Provider} from 'react-redux';

import './index.css';
import registerServiceWorker from './registerServiceWorker';
import App from './App';
import reducers from './redux/reducers';

const store = createStore(reducers);

ReactDOM.render(
    <Provider store={store}>
        <MuiThemeProvider>
            <BrowserRouter>
                <Route path="/" component={App}/>
            </BrowserRouter>
        </MuiThemeProvider>
    </Provider>,
    document.getElementById('root'));
registerServiceWorker();
