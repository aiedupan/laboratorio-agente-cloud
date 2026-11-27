import unittest
from tasks import agregar_tarea, completar_tarea, eliminar_tarea, pendientes


class TestTasks(unittest.TestCase):
    def test_agregar_tarea(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer documentación", "Estudio")
        self.assertEqual(tarea["titulo"], "Leer documentación")
        self.assertFalse(tarea["completada"])

    def test_completar_tarea(self):
        tareas = []
        agregar_tarea(tareas, "Practicar", "Estudio")
        completar_tarea(tareas, 1)
        self.assertEqual(pendientes(tareas), [])

    def test_agregar_tarea_categoria_valida(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer documentación", "  Estudio  ")
        self.assertEqual(tarea["categoria"], "Estudio")

    def test_agregar_tarea_categoria_vacia(self):
        tareas = []
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Leer documentación", "")
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Leer documentación", "   ")
        self.assertEqual(tareas, [])

    def test_filtrar_pendientes_por_categoria(self):
        tareas = []
        agregar_tarea(tareas, "Leer capítulo", "estudio")
        agregar_tarea(tareas, "Comprar café", "Hogar")
        self.assertEqual(
            [t["titulo"] for t in pendientes(tareas)],
            ["Leer capítulo", "Comprar café"],
        )
        filtradas = pendientes(tareas, "Estudio")
        self.assertEqual([t["titulo"] for t in filtradas], ["Leer capítulo"])
        self.assertEqual(filtradas[0]["categoria"], "estudio")

    def test_filtrar_categoria_inexistente(self):
        tareas = []
        agregar_tarea(tareas, "Leer capítulo", "Estudio")
        self.assertEqual(pendientes(tareas, "categoria-que-no-existe"), [])

    def test_eliminar_tarea_existente(self):
        tareas = []
        agregar_tarea(tareas, "Primera", "Estudio")
        agregar_tarea(tareas, "Segunda", "Hogar")
        agregar_tarea(tareas, "Tercera", "Laboratorio")
        eliminada = eliminar_tarea(tareas, 2)
        self.assertEqual(eliminada["id"], 2)
        self.assertEqual(eliminada["titulo"], "Segunda")
        self.assertEqual([t["id"] for t in tareas], [1, 3])
        self.assertEqual([t["titulo"] for t in tareas], ["Primera", "Tercera"])

    def test_eliminar_tarea_inexistente(self):
        tareas = []
        agregar_tarea(tareas, "Primera", "Estudio")
        antes = [dict(tarea) for tarea in tareas]
        with self.assertRaises(ValueError):
            eliminar_tarea(tareas, 99)
        self.assertEqual(tareas, antes)


if __name__ == "__main__":
    unittest.main()
