import { View, Text, ScrollView, StyleSheet } from "react-native";
import React, { useState, useEffect } from "react";
import {
  TextInput,
  Button,
  Snackbar,
  HelperText,
  List,
} from "react-native-paper";

import MaterialServices from "../../../services/MaterialServices";

const NuevoMaterialScreen = ({ route, navigation }) => {
  const { detalleMaterial, isEditar } = route.params;

  const [titulo, setTitulo] = useState(
    detalleMaterial ? detalleMaterial.titulo : ""
  );
  const [editorial, setEditorial] = useState(
    detalleMaterial ? detalleMaterial.editorial[0].nombre : ""
  );
  const [autor, setAutor] = useState(
    detalleMaterial ? detalleMaterial.autor.nombre : ""
  );
  const [carrera, setCarrera] = useState(
    detalleMaterial ? detalleMaterial.carrera : ""
  );
  const [genero, setGenero] = useState(
    detalleMaterial ? detalleMaterial.titulo : ""
  );
  console.log(detalleMaterial);
  const [editoriales, setEditoriales] = useState([]);
  const [autores, setAutores] = useState([]);
  const [carreras, setCarreras] = useState([]);
  const [generos, setGeneros] = useState([]);

  const [filteredEditoriales, setFilteredEditoriales] = useState([]);
  const [filteredAutores, setFilteredAutores] = useState([]);
  const [filteredCarreras, setFilteredCarreras] = useState([]);
  const [filteredGeneros, setFilteredGeneros] = useState([]);

  const [snackbarVisible, setSnackbarVisible] = useState(false);

  useEffect(() => {
    // Cargar datos para los campos
    const fetchData = async () => {
      try {
        if (isEditar && detalleMaterial) {
          setEditorial(
            detalleMaterial.editorial.length > 0
              ? detalleMaterial.editorial[0].nombre
              : ""
          );
          setAutor(
            detalleMaterial.autor.length > 0
              ? `${detalleMaterial.autor[0].nombre} ${detalleMaterial.autor[0].apellido}`
              : ""
          );
          setCarrera(
            detalleMaterial.carrera.length > 0
              ? detalleMaterial.carrera[0].nombre
              : ""
          );
          setGenero(
            detalleMaterial.genero.length > 0
              ? detalleMaterial.genero[0].nombre
              : ""
          );
          navigation.setOptions({
            title: "Editar Material",
          });
        }
        const responseEditoriales = await MaterialServices.listarEditoriales();
        const responseAutores = await MaterialServices.listarAutores();
        const responseCarreras = await MaterialServices.listarCarreras();
        const responseGeneros = await MaterialServices.listarGeneros();

        setEditoriales(responseEditoriales);
        setAutores(responseAutores);
        setCarreras(responseCarreras);
        setGeneros(responseGeneros);
      } catch (error) {
        console.error("Error al cargar datos:", error);
      }
    };

    fetchData();
  }, [detalleMaterial]);

  const handleGuardarMaterial = () => {
    
    setSnackbarVisible(true);
  };

  const renderDynamicInputs = (data, selectedValue, setFunction) => {
    return data.map((item) => (
      <List.Item
        key={item.id}
        title={item.nombre}
        onPress={() => setFunction(item.nombre)}
        style={{
          backgroundColor: selectedValue === item.nombre ? "#eee" : "#fff",
        }}
      />
    ));
  };
  const filterItems = (text, items) => {
    return text
      ? items.filter(
          (item) =>
            item.nombre.toLowerCase().includes(text.toLowerCase()) ||
            item.id.toString().includes(text)
        )
      : [];
  };
  const filterAutores = (text) => {
    const filtered = filterItems(text, autores);
    setFilteredAutores(filtered);
  };
  const selectAutor = (selectedAutor) => {
    setAutor(selectedAutor.nombre);
    setFilteredCarreras([]);
  };

  const filterCarreras = (text) => {
    const filtered = filterItems(text, carreras);
    setFilteredCarreras(filtered);
  };
  const selectCarrera = (selectedCarrera) => {
    setCarrera(selectedCarrera.nombre);
    setFilteredCarreras([]);
  };

  const filterGeneros = (text) => {
    const filtered = filterItems(text, generos);
    setFilteredGeneros(filtered);
  };
  const selectGenero = (selectedGenero) => {
    setGenero(selectedGenero.nombre);
    setFilteredGeneros([]);
  };

  const filterEditoriales = (text) => {
    const filtered = filterItems(text, editoriales);
    setFilteredEditoriales(filtered);
  };
  const selectEditorial = (selectedEditorial) => {
    setEditorial(selectedEditorial.nombre);
    setFilteredEditoriales([]);
  };
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <TextInput
        label="Título"
        value={titulo}
        onChangeText={(text) => setTitulo(text)}
      />
      <TextInput
        label="Editorial"
        value={editorial}
        onChangeText={(text) => {
          setEditorial(text);
          filterEditoriales(text);
        }}
      />

      {editorial.length > 0 && (
        <List.Section>
          {renderDynamicInputs(editoriales, editorial, setEditorial)}
        </List.Section>
      )}
      <TextInput
        label="Autor"
        value={autor}
        onChangeText={(text) => {
          setAutor(text);
          filterAutores(text);
        }}
      />

      <List.Section>
        {filteredAutores.map((item) => (
          <List.Item
            key={item.id}
            title={item.nombre}
            onPress={() => selectAutor(item)}
          />
        ))}
      </List.Section>

      <TextInput
        label="Carrera"
        value={carrera}
        onChangeText={(text) => {
          setCarrera(text);
          filterCarreras(text);
        }}
      />

      <List.Section>
        {filteredCarreras.map((item) => (
          <List.Item
            key={item.id}
            title={item.nombre}
            onPress={() => selectCarrera(item)}
          />
        ))}
      </List.Section>

      <TextInput
        label="Género"
        value={genero}
        onChangeText={(text) => {
          setGenero(text);
          filterGeneros(text);
        }}
      />

      <List.Section>
        {filteredGeneros.map((item) => (
          <List.Item
            key={item.id}
            title={item.nombre}
            onPress={() => selectGenero(item)}
          />
        ))}
      </List.Section>

      <Button style={styles.button} onPress={handleGuardarMaterial}>
        Guardar Material
      </Button>

      <Snackbar
        visible={snackbarVisible}
        onDismiss={() => setSnackbarVisible(false)}
      >
        Material guardado con éxito.
      </Snackbar>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  button: {
    marginTop: 16,
  },
});

export default NuevoMaterialScreen;
