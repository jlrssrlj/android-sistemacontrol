
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "../screens/home/Homescreen";
import ArqueoScreen from "../screens/arqueo/arqueoScreens";

const Stack = createNativeStackNavigator();

export default function CajeroNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Arqueo" component={ArqueoScreen} />
    </Stack.Navigator>
  );
}