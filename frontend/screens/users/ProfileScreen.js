import { View, Text } from "react-native";
import React from "react";
import { useUser } from "../../contexts/UserContext";

const ProfileScreen = () => {
  const { userInfo } = useUser();
  console.log("user: ", userInfo);
  return (
    <View>      
      {userInfo && (
        <>          
          <Text>Email: {userInfo.user.email}</Text>
          <Text>Rol: {userInfo.user.role}</Text>
        </>
      )}
    </View>
  );
};

export default ProfileScreen;
