from fastapi import HTTPException
from schemas import AnotacionCreate
from models import AnotacionDB, DetallePedidoDB, InventarioDB, PedidoDB
from sqlalchemy.orm import Session

def calcular_subtotal(detalle_pedido):
    return detalle_pedido.cantidad * detalle_pedido.precio_unitario

def actualizar_subtotal(detalle_pedido_id: int, db: Session):
    try:
        detalle_pedido = db.query(DetallePedidoDB).filter(DetallePedidoDB.id == detalle_pedido_id).first()
        if detalle_pedido is None:
            raise ValueError("Detalle de pedido no encontrado")
        detalle_pedido.subtotal = calcular_subtotal(detalle_pedido)
        db.commit()
        db.refresh(detalle_pedido)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def calcular_total_pedido(pedido_id: int, db: Session):
    try:
        detalles_pedido = db.query(DetallePedidoDB).filter(DetallePedidoDB.pedido_id == pedido_id).all()
        if not detalles_pedido:
            return 0
        total = sum(detalle.subtotal for detalle in detalles_pedido)
        return total
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def actualizar_total_pedido(pedido_id: int, db: Session):
    try:
        total = calcular_total_pedido(pedido_id, db)
        pedido = db.query(PedidoDB).filter(PedidoDB.id == pedido_id).first()
        if pedido is None:
            raise ValueError("Pedido no encontrado")
        pedido.total = total
        db.commit()
        db.refresh(pedido)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def actualizar_pedido(detalle_pedido_id: int, db: Session):
    actualizar_subtotal(detalle_pedido_id, db)
    detalle_pedido = db.query(DetallePedidoDB).filter(DetallePedidoDB.id == detalle_pedido_id).first()
    pedido_id = detalle_pedido.pedido_id
    actualizar_total_pedido(pedido_id, db)
    actualizar_inventario(pedido_id, db)

def actualizar_inventario(detalle_pedido_id: int, db: Session):
    detalle_pedido= db.query(DetallePedidoDB).filter(DetallePedidoDB.id == detalle_pedido_id).first()
    if detalle_pedido is None:
        # Manejar el caso en que no se encuentra el detalle de pedido
        raise ValueError(f"No se encontró el detalle de pedido con ID {detalle_pedido_id}")
    producto_id=  detalle_pedido.producto_id
    cantidad = detalle_pedido.cantidad

    inventario= db.query(InventarioDB).filter(InventarioDB.producto_id==producto_id).first()
    if inventario is None:
        # Manejar el caso en que no se encuentra el detalle de inventario
        raise ValueError(f"No se encontró el producto en inventario con ID {producto_id}")
    
    inventario.cantidad -= cantidad
    if inventario.cantidad <0:
        raise("No hay cantidades suficientes")
    db.commit
    db.refresh(inventario)

def agregar_anotacion_pedido(pedido_id: int, anotacion: AnotacionCreate, db: Session):
    db_anotacion = AnotacionDB(**anotacion.dict(), pedido_id=pedido_id)
    db.add(db_anotacion)
    db.commit()
    db.refresh(db_anotacion)
    return db_anotacion