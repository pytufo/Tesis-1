import {
  View,
  Text,
  TextInput,
  Button,
  FlatList,
  StyleSheet,
  TouchableOpacity,
  Keyboard,
} from "react-native";
import React, { useEffect, useState } from "react";
import { useRoute } from "@react-navigation/native";
import { useUser } from "../../contexts/UserContext";
import MovimientosServices from "../../services/MovimientosServices";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";
import axios from "axios";
import { toast } from "react-toastify";
import moment from "moment";

const DetalleReservaScreen = () => {
  const route = useRoute();
  const [detalleReserva, setDetalleReserva] = useState({});
  const [ejemplaresDisponibles, setEjemplaresDisponibles] = useState([]);
  const [selectedEjemplar, setSelectedEjemplar] = useState();
  const { reservaId } = route.params;
  const [searchText, setSearchText] = useState("");
  const [filteredEjemplares, setFilteredEjemplares] = useState([]);

  const { userInfo } = useUser();
  const accessToken = userInfo.access_token;
  useEffect(() => {
    const fetchDetalleReserva = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.RESERVAS}${reservaId}/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setDetalleReserva(response.data || {});
        console.log(response.data);
      } catch (error) {
        console.error("Error al obtener los datos de la reserva");
      }
    };

    const fetchEjemplaresDisponibles = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.RESERVAS}${reservaId}/entregar_ejemplar/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setEjemplaresDisponibles(response.data.ejemplares_disponibles);
        console.log(response.data);
      } catch (error) {
        console.error("Error al obtener los ejemplares disponibles");
      }
    };
    fetchEjemplaresDisponibles();
    fetchDetalleReserva();
  }, [reservaId, accessToken]);

  const handleEntregarEjemplar = async () => {
    try {
      const access_token = userInfo.access_token;

      if (!selectedEjemplar || !searchText) {
        toast.error("Seleccciona un ejemplar a entregar");
        return;
      }
      const ejemplarExist = ejemplaresDisponibles.some(
        (ejemplar) => ejemplar.id === selectedEjemplar
      );

      if (!ejemplarExist) {
        toast.error("El ejemplar seleccionado ya no está disponible");
        return;
      }
      const owner_id = detalleReserva.owner.id;

      const prestamoData = {
        created_by: userInfo.user.id,
        owner: owner_id,
        ejemplar: selectedEjemplar,
      };
      const response = await MovimientosServices.entregarEjemplarReserva(
        access_token,
        reservaId,
        prestamoData
      );
      console.log(response);

      toast.info(response.message);
    } catch (error) {
      console.error("Error al entregar el ejemplar");
    }
  };

  const handleSearchChange = (text) => {
    setSearchText(text);
    const filtered = ejemplaresDisponibles.filter((ejemplar) =>
      ejemplar.id.toString().includes(text)
    );
    setFilteredEjemplares(filtered);
  };
  const handleEjemplarSelect = (ejemplarId) => {
    setSelectedEjemplar(ejemplarId);
    const selectedEjemplar = ejemplaresDisponibles.find(
      (ejemplar) => ejemplar.id === ejemplarId
    );
    setSearchText(selectedEjemplar?.id.toString() || "");
  };
  const handleKeyboardDismiss = () => {
    Keyboard.dismiss();
  };
  const handleKeyPress = ({ nativeEvent }) => {
    const { key } = nativeEvent;
    if (key === "ArrowDown" || key === "ArrowUp") {
      // Navegación hacia arriba o abajo en la lista de ejemplares
      const currentIndex = filteredEjemplares.findIndex(
        (ejemplar) => ejemplar.id === selectedEjemplar
      );

      const newIndex =
        key === "ArrowDown"
          ? (currentIndex + 1) % filteredEjemplares.length
          : (currentIndex - 1 + filteredEjemplares.length) %
            filteredEjemplares.length;

      handleEjemplarSelect(filteredEjemplares[newIndex].id);
    }
  };

  return (
    <View style={styles.container} onTouchStart={handleKeyboardDismiss}>
      {detalleReserva ? (
        <View style={styles.reservaContainer}>
          <Text>Detalles de la reserva</Text>
          <Text>Solicitante:{detalleReserva.owner?.email}</Text>
          <Text>Material: {detalleReserva.material?.titulo}</Text>
          <Text>
            Finalizacion:{" "}
            {moment(detalleReserva.fecha_fin).format("YYYY-MM-DD HH:mm:ss")}
          </Text>
          {detalleReserva.estado === "Finalizada" ? (
            <Text style={styles.finalizadaText}> Finalizada</Text>
          ) : (
            <View style={styles.entregarContainer}>
              <Text style={styles.label}>Buscar ejemplar por ID: </Text>
              <TextInput
                style={styles.input}
                value={searchText}
                onChangeText={handleSearchChange}
                placeholder="Ingresa el ID del ejemplar"
                defaultValue={selectedEjemplar?.toString()}
                onKeyPress={handleKeyPress}
              />
              <FlatList
                style={styles.flatList}
                data={filteredEjemplares}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }) => (
                  <TouchableOpacity
                    onPress={() => handleEjemplarSelect(item.id)}
                    style={[
                      styles.ejemplarItem,
                      item.id === selectedEjemplar && styles.selectedItem,
                    ]}
                  >
                    <Text
                      style={styles.ejemplarText}
                    >{`ID: ${item.id}, Estado: ${item.estado}`}</Text>
                  </TouchableOpacity>
                )}
              />

              <Button
                style={styles.button}
                title="Entregar ejemplar"
                onPress={handleEntregarEjemplar}
              />
            </View>
          )}
        </View>
      ) : (
        <Text>Cargando reserva...</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 16,
  },
  reservaContainer: {
    width: "100%",
  },
  finalizadaText: {
    fontWeight: "bold",
    color: "green",
    marginBottom: 10,
  },
  entregarContainer: {
    marginTop: 10,
  },
  label: {
    fontSize: 16,
    marginBottom: 5,
  },
  input: {
    height: 40,
    borderColor: "gray",
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
  },
  flatList: {
    marginBottom: 10,
  },
  ejemplarText: {
    fontSize: 16,
  },
  button: {
    marginTop: 10,
  },
  loadingText: {
    fontSize: 18,
    fontStyle: "italic",
  },
  ejemplarItem: {
    padding: 10,
    borderBottomWidth: 1,
    borderColor: "#ccc",
  },
  selectedItem: {
    backgroundColor: "#e0e0e0",
  },
});

export default DetalleReservaScreen;
