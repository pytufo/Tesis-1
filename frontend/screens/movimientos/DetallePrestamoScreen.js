import {
  View,
  Text,
  FlatList,
  StyleSheet,
  TouchableOpacity,
  Keyboard,
} from "react-native";
import {
  Button,
  Dialog,
  PaperProvider,
  Paragraph,
  Portal,
  TextInput,
} from "react-native-paper";
import React, { useEffect, useState } from "react";
import { useRoute } from "@react-navigation/native";
import { useUser } from "../../contexts/UserContext";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";
import MovimientosServices from "../../services/MovimientosServices";
import { toast } from "react-toastify";
import moment from "moment";
const DetallePrestamoScreen = () => {
  const route = useRoute();
  const [detallePrestamo, setDetallePrestamo] = useState(null);
  const { prestamoId } = route.params;

  const [dialogVisible, setDialogVisible] = useState(false);

  const { userInfo } = useUser();

  useEffect(() => {
    const fetchDetallePrestamo = async () => {
      try {
        const accessToken = userInfo.access_token;
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.PRESTAMOS}${prestamoId}/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setDetallePrestamo(response.data || {});
        console.log(response.data);
      } catch (error) {
        console.error("Error al obtener los datos del prestamo");
      }
      console.log(detallePrestamo.ejemplar.material.titulo);
    };
    fetchDetallePrestamo();
  }, [prestamoId, userInfo]);

  const handleConfirmar = async () => {
    setDialogVisible(true);
  };
  const handleCancel = () => {
    // Cerrar el diálogo de confirmación
    setDialogVisible(false);
  };

  const handleFinalizarPrestamo = async () => {
    try {
      const access_token = userInfo.access_token;

      const response = await MovimientosServices.finalizarPrestamo(
        access_token,
        prestamoId
      );
      console.log(response);

      if (response.ok) {
        setDialogVisible(false);
        toast.info("Devolucion exitosa");
      } else {
        setDialogVisible(false);
        toast.error("Error al realizar la devolucion");
      }
    } catch (error) {
      toast.error("Error al finalizar el prestamo");
    }
    
  };
  return (
    <PaperProvider>
      <View style={styles.container}>
        {detallePrestamo ? (
          <View style={styles.reservaContainer}>
            <Text> Entregado por: {detallePrestamo.created_by}</Text>
            <Text> Usuario: {detallePrestamo.owner?.email}</Text>
            <Text> Ejemplar: {detallePrestamo.ejemplar?.id} </Text>

            <Text> Material: </Text>
            <Text> {detallePrestamo.ejemplar?.material[0]?.titulo} </Text>
            <Text>
              {" "}
              Finalizacion:{" "}
              {moment(detallePrestamo.fecha_fin).format("YYYY-MM-DD HH:mm:ss")}
            </Text>
            {detallePrestamo.estado === "Finalizado" ? (
              <Text>Prestamo Finalizado</Text>
            ) : (
              <View style={styles.entregarContainer}>
                {userInfo && userInfo.user.role === 1 ? (
                  <View style={styles.entregarContainer}>
                    <Button style={styles.button} onPress={handleConfirmar}>
                      <Text style={[styles.buttonText, { color: "#FFFFFF" }]}>
                        Finalizar prestamo
                      </Text>
                    </Button>
                    <Portal>
                      <Dialog
                        visible={dialogVisible}
                        onDismiss={handleConfirmar}
                      >
                        <Dialog.Content>
                          <Paragraph>¿Quieres finalizar el prestamo?</Paragraph>
                        </Dialog.Content>
                        <Dialog.Actions>
                          <Button onPress={handleCancel}>Cancelar</Button>
                          <Button onPress={handleFinalizarPrestamo}>
                            Aceptar
                          </Button>
                        </Dialog.Actions>
                      </Dialog>
                    </Portal>
                  </View>
                ) : (
                  <></>
                )}
              </View>
            )}
          </View>
        ) : (
          <Text>Cargando prestamo...</Text>
        )}
      </View>
    </PaperProvider>
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
    backgroundColor: "#2471A3",
    marginTop: 10,
  },
  buttonText: {
    color: "#FFFFFF",
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

export default DetallePrestamoScreen;
