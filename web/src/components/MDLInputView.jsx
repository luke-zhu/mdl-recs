import React from 'react';
import PropTypes from 'prop-types';
import TextField from 'material-ui/TextField';
import {connect} from 'react-redux';

import {
  showLoading,
  getMyShows,
  getSimilarShows,
} from '../redux/actions';

const style = {
  'margin': 20,
};

const MDLInputView = ({handleKeyPress}) => (
    <div style={style}>
      <TextField
          floatingLabelText="Enter your MDL username here."
          onKeyPress={handleKeyPress}
      />
    </div>
);

MDLInputView.propTypes = {
  handleKeyPress: PropTypes.func.isRequired,
};

const mapDispatchToProps = dispatch => ({
  handleKeyPress: (e) => {
    if (e.key === 'Enter') {
      console.log('Username entered');
      console.log('Migrating!');
      dispatch(showLoading());
    }
  },
});

export default connect(null, mapDispatchToProps)(MDLInputView);
