import React from 'react';
import AppBar from 'material-ui/AppBar';

import MDLInputView from './components/MDLInputView.jsx';
import ShowList from './components/ShowList.jsx';
import HighlightList from './components/HighlightList.jsx';

class App extends React.Component {
  render() {
    return (
        <div>
          <AppBar
              title={'MDL Recs'}
              showMenuIconButton={false}
          />
          <div style={{display: 'flex', alignContent: 'stretch'}}>
            <div>
              <MDLInputView/>
              <ShowList/>
            </div>
            <div style={{minWidth: '100%', backgroundColor: '#E0F7FA'}}>
              <HighlightList/>
            </div>
          </div>
        </div>
    );
  }
}

export default App;
