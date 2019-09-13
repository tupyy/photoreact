import React from 'react';
import {connect} from 'react-redux';
import {IRootState} from "app/shared/reducers";
import UserAvatar from "app/shared/components/user_avatar/user-avatar";
import UserProfileHeader from "app/modules/user-profile/components/user-profile-header";
import {getFullName} from "app/shared/util/user-name-utils";
import UserProfileTabs from "app/modules/user-profile/components/user-profile-tabs";

interface IUserProfileProps extends StateProps {

}

const TabNames = ["Overview", "Activity", "Albums", "Permissions"];

/**
 * Return an user avatar component
 */
const getUserAvatarComponent = (userProfile) => {
    return (
        <UserAvatar
            firstName={userProfile.first_name}
            lastName={userProfile.last_name}
            profilePhoto={userProfile.photo}
            size="xl"
        />
    )
};

/**
 * Main component to show the user profile.
 */
const UserProfile = (props: IUserProfileProps) => {

    const handleTabChange = (event, newValue) => {
       console.log("Tab changed: " + String(newValue));
    };

    return (
        <div>
            <UserProfileHeader
                avatarComponent={getUserAvatarComponent(props.account)}
                title={getFullName(props.account.first_name, props.account.last_name)}
            />
            <UserProfileTabs
                tabNames={TabNames}
                handleTabChange={handleTabChange}
            />
        </div>
    )
};

const mapStateToProps = ({authentication}: IRootState) => ({
    account: authentication.account
});

type StateProps = ReturnType<typeof mapStateToProps>;

export default connect(
    mapStateToProps
)(UserProfile)
