import React, { PropTypes } from 'react';
import TextField from 'material-ui/TextField';
import { Meteor } from 'meteor/meteor';
import { connect } from 'react-redux';

import { getMyShows } from '../redux/actions';

const MDLInputView = ({ handleKeyPress }) => (
  <div>
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
      Meteor.call('mdl.getList', e.target.value, (error, result) => {
        if (error) console.error(error);
        else dispatch(getMyShows(result));
      });
      Meteor.call('shows.getTop', 20, (error, result) => {
        if (error) console.error(error);
        else console.log(result);
      });
    }
  },
});

export default connect(null, mapDispatchToProps)(MDLInputView);
