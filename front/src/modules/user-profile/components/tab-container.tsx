import React from 'react';
import {Container} from "@material-ui/core";
import {ComponentArray, ITabComponent} from "app/modules/user-profile/tab-component-interface";

interface ITabContainer {
    components: ComponentArray
}

const TabContainer = (props: ITabContainer) => {
    return (
        <Container>
        {props.components.map( ( TabComponent: React.SFC<ITabComponent>, index: number) =>
                <TabComponent
                    index={index}
                    key={String(index)}
                />
        )}
        </Container>

    )
};

export default TabContainer;
