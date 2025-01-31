# 📦 Consultar existencias de productos

Revisa las existencias de los productos antes de realizar la entrega de algún producto.

## 🚀 Compatible con versiones de Odoo  
Este módulo es compatible con *Odoo Community 12.0*.

🔗 [Repositorio en GitHub](https://github.com/AlfaSystemas5457/check_stock)

---

## ⚙ Funcionamiento

En caso de que no exista stock suficiente, se procede a realizar una venta parcial.

Por ejemplo:

De este producto solo hay 10 en existencia.

![A la mano.png](./static/description/assets/A%20la%20mano.png)

Si se realiza una compra mayor a la existencia del producto, se podrá facturar.

![Ejemplo de compra.png](./static/description/assets/Ejemplo%20de%20compra.png)

Sin embargo, al momento de validar la entrega, aparecerá un error debido a la falta de existencias del producto.

![Validar pedido.png](./static/description/assets/Validar%20pedido.png)

Este es el error de validación. Odoo ajustará automáticamente la cantidad de producto disponible, permitiendo una entrega parcial.

![Error de validación.png](./static/description/assets/Error%20de%20validación.png)

Si no hay existencias del producto, aparecerá un error. En este caso, Odoo no ajustará automáticamente la cantidad en entrega y no permitirá continuar hasta que haya stock disponible.

![Error de validación sin stock.png](./static/description/assets/Error%20de%20validación%20sin%20stock.png)

## 📥 Instalación

Para instalar este módulo, sigue estos pasos:

- Descargar el repositorio:

```bash
git clone https://github.com/AlfaSystemas5457/check_stock.git
```
- Copiar la carpeta del módulo en la ruta de addons de Odoo.
- Actualizar la lista de módulos en Odoo.
- Instalar el módulo desde la interfaz de Odoo.