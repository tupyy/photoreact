import React from 'react';

export interface ITabComponent {
    index: number
}

export type ComponentArray = Array<React.SFC<ITabComponent>>;
