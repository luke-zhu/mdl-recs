import React from 'react';
import AppBar from 'material-ui/AppBar';

import MDLInputView from './components/MDLInputView.jsx';
import MDLShowsList from './components/MDLShowsList.jsx';

const testShows = [
  { name: 'Age of Youth' },
  { name: 'Incomplete Life' },
  { name: 'Doggo' },
];

const App = () => (
  <div>
    <AppBar
      title="MDL Recs"
      showMenuIconButton={false}
    />
    <MDLInputView />
    <MDLShowsList />
  </div>
);

export default App;
