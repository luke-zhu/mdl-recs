import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';

import RecommendedShows from './RecommendedShows.jsx';
import LoadingView from './LoadingView.jsx';

const MDLShowsList = ({loading, myShows, similarShows}) => {
    if (!loading) {
        return null;
    } else if (myShows.length === 0) {
        return <LoadingView caption={'Loading your shows'}/>;
    } else if (similarShows.length === 0) {
        return <LoadingView caption={'Finding similar shows'}/>;
    }
    return (
        <RecommendedShows
            myShows={myShows}
            similarShows={similarShows}
        />
    );
};

MDLShowsList.propTypes = {
    loading: PropTypes.bool.isRequired,
    myShows: PropTypes.array.isRequired,
    similarShows: PropTypes.array.isRequired,
};

const mapStateToProps = state => ({
    loading: state.loading,
    myShows: state.myShows,
    similarShows: state.similarShows,
});

export default connect(mapStateToProps)(MDLShowsList);
