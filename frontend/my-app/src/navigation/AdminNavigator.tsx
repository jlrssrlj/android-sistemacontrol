import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "../screens/home/Homescreen";
import MedioPagoScreen from "../screens/mediospago/MedioPagoScreens";

const Stack = createNativeStackNavigator();

export default function AdminNavigatos(){
    return(
        <Stack.Navigator>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="MediosPago" component={MedioPagoScreen} />

        </Stack.Navigator>
    )
}