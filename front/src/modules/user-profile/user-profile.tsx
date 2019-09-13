import React, {useState} from 'react';
import {connect} from 'react-redux';
import {IRootState} from "app/shared/reducers";
import UserAvatar from "app/shared/components/user_avatar/user-avatar";
import UserProfileHeader from "app/modules/user-profile/components/user-profile-header";
import {getFullName} from "app/shared/util/user-name-utils";
import UserProfileTabs from "app/modules/user-profile/components/user-profile-tabs";
import {TabContext} from "app/modules/user-profile/tab-context";
import {Overview} from "app/modules/user-profile/components/overview";
import TabContainer from "app/modules/user-profile/components/tab-container";
import {ComponentArray} from "app/modules/user-profile/tab-component-interface";
import Activity from "app/modules/user-profile/components/activities";
import AlbumsTab from "app/modules/user-profile/components/albums-tab";
import PermissionsTab from "app/modules/user-profile/components/permissions-tab";

interface IUserProfileProps extends StateProps {

}

// define the names of the tab
const TabNames = ["Overview", "Activity", "Albums", "Permissions"];

// define the components which ill be render in the tab container
const TabComponents: ComponentArray = [Overview, Activity, AlbumsTab, PermissionsTab];
const contextValue = {
   albumTab: {
       url:"/api/albums?limit=5"
   },
   activityTab: {
       url:"/api/activity"
   }
}
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
    const [currentTab, setCurrentTab] = useState(0);

    const handleTabChange = (newValue) => {
        console.log("Tab changed: " + String(newValue));
        setCurrentTab(newValue);
    };

    return (
        <div>
            <UserProfileHeader
                avatarComponent={getUserAvatarComponent(props.account)}
                title={getFullName(props.account.first_name, props.account.last_name)}
            />
            <UserProfileTabs
                tabNames={TabNames}
                handleChange={handleTabChange}
            />
            <TabContext.Provider 
                value={{
                    currentTab: currentTab,
                    ...contextValue
                }}
            >
                <TabContainer components={TabComponents}/>
            </TabContext.Provider>
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
