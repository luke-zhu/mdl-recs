import React, { PropTypes } from 'react';
import Paper from 'material-ui/Paper';
import CircularProgress from 'material-ui/CircularProgress';

const LoadingView = ({ caption }) => (
  <Paper style={{ padding: 10, marginBottom: 20 }} zDepth={2}>
    <CircularProgress />
    <h4>{caption}</h4>
  </Paper>
);

LoadingView.propTypes = {
  caption: PropTypes.string,
};

export default LoadingView;
