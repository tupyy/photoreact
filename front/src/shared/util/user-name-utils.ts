export const getFullName = (firstName: string, lastName: string): string => {
   if (firstName && lastName) {
        return capitalizeFirstLetter(firstName) + firstName.slice(1) +
            ' ' + capitalizeFirstLetter(lastName) + lastName.slice(1);
   }
   return '';
};

export const getNameInitials = (firstName: string, lastName: string): string => {
    if (firstName && lastName) {
        return capitalizeFirstLetter(firstName) + capitalizeFirstLetter(lastName);
    } else {
        return '';
    }
};

const capitalizeFirstLetter = (word: string) : string => {
    return word.charAt(0).toUpperCase();
};
