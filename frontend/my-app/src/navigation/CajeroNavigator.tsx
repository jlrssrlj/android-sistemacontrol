
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "../screens/home/Homescreen";

const Stack = createNativeStackNavigator();

export default function CajeroNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" component={HomeScreen} />
    </Stack.Navigator>
  );
}