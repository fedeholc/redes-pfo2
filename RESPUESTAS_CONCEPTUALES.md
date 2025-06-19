# Programación sobre Redes - 3°B

## PFO2 - Sistema de Gestión de Tareas con API y Base de Datos

**Estudiante: Federico Holc**

# Respuestas Conceptuales

## ¿Por qué hashear contraseñas?

Hashear contraseñas es una práctica fundamental para la seguridad de cualquier sistema que almacene credenciales de usuarios. Cuando una contraseña se almacena en forma de hash, incluso si un atacante logra acceder a la base de datos, no podrá ver las contraseñas reales, ya que los hashes son irreversibles y no permiten obtener la contraseña original. Además, ni siquiera el administrador del sistema puede conocer las contraseñas de los usuarios, lo que añade una capa extra de privacidad y protección.

El uso de algoritmos como bcrypt, que incluyen un "salt" único para cada contraseña, protege contra ataques de diccionario y de fuerza bruta, ya que el salt previene el uso de rainbow tables (tablas de hashes precalculados) y el propio algoritmo es computacionalmente costoso, haciendo que los intentos de adivinar contraseñas sean muy lentos. Hashear contraseñas también es un requisito de muchas regulaciones y estándares de la industria, como el GDPR y las recomendaciones de OWASP, que exigen la protección adecuada de los datos personales y el cifrado de información sensible.

Por último, almacenar solo el hash de la contraseña permite al sistema cumplir con el principio de responsabilidad mínima: solo necesita verificar si una contraseña es correcta, sin necesidad de almacenarla en texto plano. Esto reduce la responsabilidad legal en caso de una violación de datos y protege la privacidad de los usuarios.

## Ventajas de usar SQLite en este proyecto

SQLite ofrece múltiples ventajas que lo hacen ideal para este tipo de proyecto. En primer lugar, destaca por su simplicidad y facilidad de implementación: no requiere la instalación de un servidor de base de datos, ya que toda la información se almacena en un único archivo (`tareas.db`). Esto elimina la necesidad de configuraciones complejas o dependencias externas, permitiendo una integración directa y sin servicios adicionales.

Otra ventaja clave es su portabilidad. SQLite funciona de manera idéntica en Windows, macOS y Linux, y trasladar la base de datos a otro entorno es tan sencillo como copiar un archivo. Esto facilita tanto la transferencia como el respaldo y el versionado de la base de datos, lo que resulta especialmente útil durante el desarrollo.

En cuanto al rendimiento, SQLite es muy eficiente para operaciones de lectura y consume pocos recursos, lo que lo hace perfecto para aplicaciones pequeñas o medianas como la de este proyecto. Al no requerir comunicación cliente-servidor, elimina la latencia de red y está optimizado para aplicaciones locales.

Desde el punto de vista técnico, SQLite cumple con las propiedades ACID (Atomicidad, Consistencia, Aislamiento y Durabilidad), lo que garantiza la integridad de los datos incluso en operaciones complejas o concurrentes. Utiliza una sintaxis SQL estándar, lo que facilita la migración a otros sistemas de bases de datos en el futuro y permite el uso de funcionalidades avanzadas como JOINs, índices y triggers. Además, maneja automáticamente la concurrencia, permitiendo que varias conexiones accedan a la base de datos de forma segura.

Para el desarrollo y prototipado, SQLite permite un desarrollo rápido, ya que no se pierde tiempo en configuraciones. Cada test puede utilizar su propia base de datos temporal, y el despliegue es tan simple como subir el archivo Python y el archivo .db. Además, el archivo de base de datos puede abrirse fácilmente con herramientas visuales para depuración.

Por todas estas razones, SQLite es especialmente adecuado para aplicaciones de escritorio, prototipos, MVPs, aplicaciones web pequeñas a medianas, móviles, sistemas embebidos, herramientas de desarrollo y almacenamiento temporal, como es el caso de este proyecto.
