## Commit estandar

**[Conventional Commits 1.0.0:](https://www.conventionalcommits.org/en/v1.0.0/)** Una especificación para agregar significado legible por humanos y máquinas a los mensajes de confirmación.

1. Cada commit debe comenzar con un pie de página de "tipo" (ver más abajo).
2. **Puede** ir seguido de un *scope* indicando lo afectado.
3. Debe ir seguido de una breve descripción.
4. **Puede** tener un cuerpo detallando los cambios.
5. **Puede** tener más pies de página después del cuerpo.

```plaintext
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Formato del commit

* **Tipo** : Debe ser todo en minúsculas. Ejemplos: `fix`, `feat`, `docs`, etc.
* **Scope** : Es opcional y también debe ser todo en minúsculas. Se refiere a la parte del código que se ve afectada por el commit. Ejemplo: `(ui)`, `(server)`, `(docs)`.
* **Descripción** : Debe ser una breve descripción de los cambios realizados. Debe comenzar con una letra minúscula y no terminar con un punto.
* **Cuerpo** : Es opcional y se utiliza para explicar los cambios realizados en detalle. Debe comenzar con una letra minúscula y no terminar con un punto.
* **Pie de página** : Es opcional y se utiliza para hacer referencia a las issues que se cierran con el commit.

#### Palabras clave del pie de página

Estos son elementos estructurales que comunican la intención del commit:

- **fix**: indica que se corrigió un error en el código.
- **feat**: indica una nueva característica en el código.
- **docs**: indica la documentación del código.
- **test**: indica prueba del código.
- **style** : indica cambios que no afectan el significado del código (espacios en blanco, formato, punto y coma faltantes, etc).
- **refactor** : indica un cambio de código que ni arregla un error ni añade una característica.
- **perf** : indica un cambio de código que mejora el rendimiento.
- **chore** : indica cambios en las tareas de construcción o herramientas auxiliares y bibliotecas.

También se permite cualquier otro si ayuda a proporcionar un mejor contexto.

#### **Ejemplos de mensajes de commit:**

```powershell
feat(user-auth): add password reset functionality

This commit adds the ability for users to reset their password. The user will receive an email with a link to reset their password.

Closes #123

```

```powershell
fix(server): fix server crash on startup

This commit fixes a bug where the server would crash on startup if the database was not reachable.

Closes #456

```

## Estandar de branch

1. **Main** : Esta es la rama principal. Contiene el código de producción, es decir, el código que está actualmente en uso en producción.
2. **Develop** : Esta es la rama de desarrollo, contiene características que podrían ser lanzadas en la próxima versión.
3. **Feature** : Cada nueva característica debe residir en su propia rama, que puede ser empujada al repositorio de desarrollo para su revisión.

```plaintext
feature/<nombre-de-la-caracteristica>
```

4. **Bugfix** : Si estás haciendo un arreglo de un bug en producción, usarías una rama bugfix.

```plaintext
bugfix/<nombre-del-bugfix>
```

5. **Hotfix** : Los hotfixes son muy similares a los bugfixes, pero representan cambios urgentes que necesitan ser aplicados en producción inmediatamente y luego mezclados tanto en `develop` como en `master`.

```plaintext
hotfix/<nombre-del-hotfix>
```

6. **Release** : Una vez que `develop` ha adquirido suficientes características para una versión (o se ha programado una fecha de lanzamiento específica), se bifurca una rama de `release`.

```plaintext
release/<nombre-de-la-version>
```


## Estilo de código

##### **PEP 8: Guía de estilo para el código Python**

Es la guía de estilo principal que proporciona convenciones para el formato del código Python, incluyendo indentación, comentarios, nombres de variables, importaciones y más. Aquí hay algunos puntos clave:

* **Indentación** : Usa 4 espacios por nivel de indentación.
* **Líneas largas** : Limita todas las líneas a un máximo de 79 caracteres.
* **Espacios en blanco** : Usa espacios en blanco de manera consistente.
* **Nombres de variables y funciones** : Usa `snake_case` para funciones y variables.
* **Nombres de clases** : Usa `CamelCase` para nombres de clases.

    **Flake8:** Herramienta para verificar el código Python en busca de errores de estilo y posibles errores.

##### DJango

 **Orden de los modelos** : Los modelos deben ser ordenados por `ForeignKey`, `ManyToManyField` y `OneToOneField`. Esto significa que cuando defines un modelo, debes listar primero los campos que son `ForeignKey`, luego los campos que son `ManyToManyField` y finalmente los campos que son `OneToOneField`.

 **Orden de las clases** : Las clases deben ser ordenadas por `Meta`, `managers`, `class methods`, `inline classes`, y finalmente `methods`. Esto significa que dentro de una clase, debes definir primero la clase `Meta`, luego los `managers`, luego los `class methods`, luego las `inline classes`, y finalmente los `methods`.

 **Orden de los métodos** : Los métodos deben ser ordenados por `CRUD operations` (Create, Retrieve, Update, Delete). Esto significa que dentro de una clase, debes definir primero los métodos que crean datos, luego los métodos que recuperan datos, luego los métodos que actualizan datos, y finalmente los métodos que eliminan datos.

    **Django-lint**: Herramienta para verificar el código Django en busca de errores de estilo y posibles errores.

##### **Object-Oriented Programming**

Este estilo de programación se centra en crear objetos que tienen propiedades y métodos. Python es un lenguaje de programación versatil que brinda la posibilidad de uso de este estilo mediante la creación de objetos y clases.

Un objeto es cualquier entidad que tenga atributos (variables) y comportamientos (métodos). Mientras que una clase es el plano para crear ese objeto.

El estilo de programación orientada a objetos también provee:

- **Herencia**: Una forma de crear clases con detalles de otra clase, ya existente, sin necesidad de modificarla. **En python se declara herencia de manera tal: "class Hija(Padre)"**
- **Encapsulamiento**: Una forma de asegurar y limitar el acceso a atributos o comportamientos exclusivos de una clase. **En python se representan atributos privados con "_" o "__"**.
- **Polimorfismo**: Una forma de dar distintos significados o comportamientos a un mismo objeto o método. en python esto se logra escribiendo un mismo método con atributos diferentes o un método en diferentes clases.
