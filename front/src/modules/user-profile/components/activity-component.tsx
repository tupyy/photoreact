import React, {useEffect} from 'react';
import { Container } from '@material-ui/core';
import ActivityItem from './activity-item';
import {IActivity} from 'app/shared/model/activity.model';
import {IRootState} from 'app/shared/reducers';
import {getActivities} from 'app/shared/reducers/user-profile';
import {connect} from 'react-redux';

interface IActivityComponent extends StateProps, DispatchProps {
    title: string,
	visible: boolean
}

/**
 * It renders the activities fetched from server. It can be embedded into Overview or Activities tabs
 */
const ActivityComponent = (props: IActivityComponent) => {

	useEffect( () => {
		// Load data only once when the tab becomes visible for the first time
		if (props.visible && !hasData(props.activities) && !props.loading ) {
			props.getActivities();
		}
	});

	const hasData = (arr: Array<IActivity>) => {
		return arr.length !== 0;
	};

	if (props.loading) {
		return <div>Loading...</div>;
	};

    return (
        <Container maxWidth="xl">
            {props.activities.map( (item: IActivity, index: number ) => 
                <ActivityItem 
                    key={String(index)}
                    id={item.content_object.id}
                    title={item.content_object.name}
                    date={item.date}
                    activity={item.activity}
                    user={item.user}
                />
            )}
        </Container>
    )
};

const mapStateToProps = ({userProfile}: IRootState) => ({
	loading: userProfile.loading,
	activities: userProfile.activities,
	errorMessage: userProfile.errorMessage
});

const mapDispatchToProps = {
	getActivities
};

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(ActivityComponent);
