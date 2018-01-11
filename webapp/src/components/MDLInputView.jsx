import React from 'react';
import PropTypes from 'prop-types';
import TextField from 'material-ui/TextField';
import {connect} from 'react-redux';

import {
  displayLoadingIcon,
  searchForShow,
} from '../redux/actions';

const style = {
  'margin': 20,
};

const MDLInputView = ({handleKeyPress}) => (
    <div style={style}>
      <TextField
          label="Search for a show."
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
      dispatch(displayLoadingIcon());
      dispatch(searchForShow(e.target.value))
    }
  },
});

export default connect(null, mapDispatchToProps)(MDLInputView);
