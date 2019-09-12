import React from 'react';
import {connect} from 'react-redux';
import {IRootState} from "app/shared/reducers";
import UserAvatar from "app/shared/components/user_avatar/user-avatar";
import UserProfileHeader from "app/modules/user-profile/components/user-profile-header";
import {getFullName} from "app/shared/util/user-name-utils";

interface IUserProfileProps extends StateProps {

}

/**
 * Main component to show the user profile.
 */
const UserProfile = (props: IUserProfileProps) => {

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

    return (
        <div>
            <UserProfileHeader
                avatarComponent={getUserAvatarComponent(props.account)}
                title={getFullName(props.account.first_name, props.account.last_name)}
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
