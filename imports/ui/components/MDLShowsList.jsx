import React, { PropTypes } from 'react';
import { connect } from 'react-redux';

import MDLCard from './MDLCard.jsx';

const MDLShowsList = ({ shows }) => {
  const rows = [];
  shows.forEach(show => rows.push(<MDLCard show={show} />));
  return <div>{rows.length === 0 ? null : <h1>Your Listed Shows</h1>}{rows}</div>;
};

MDLShowsList.propTypes = {
  shows: PropTypes.arrayOf(
    PropTypes.objectOf(
        PropTypes.string.isRequired
      ).isRequired
    ).isRequired,
};

const mapStateToProps = state => ({
  shows: state.myShows,
});

export default connect(mapStateToProps)(MDLShowsList);
