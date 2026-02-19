from PIL import Image, ImageSequence

# Configura aquí el tamaño del recorte que quieras
CROP_SIZE = 256 

with Image.open('./assets/darksign2.gif') as img:
    frames = []
    
    # Extraemos la duración original antes de empezar
    original_duration = img.info.get('duration', 100)

    for frame in ImageSequence.Iterator(img):
        
        #avoid last 10 frames that are mostly black
        if frame.tell() > img.n_frames - 30:
            break
        # 1. Convertir a RGBA
        f = frame.convert("RGBA")
        
        # 2. RECORTAR DESDE EL CENTRO
        width, height = f.size
        left = (width - CROP_SIZE) // 2
        top = (height - CROP_SIZE) // 2
        right = left + CROP_SIZE
        bottom = top + CROP_SIZE
        
        f = f.crop((left, top, right, bottom))
        
        # 3. PROCESAR TRANSPARENCIA
        # Usamos list() para asegurar que la manipulación es limpia
        datas = list(f.getdata())
        newData = []
        
        for item in datas:
            # item[0,1,2] son R, G, B. item[3] es Alpha.
            # Bajamos un poco el umbral a 20 para no borrar el fuego tenue
            if item[0] < 20 and item[1] < 20 and item[2] < 20:
                newData.append((0, 0, 0, 0)) # Transparente
            else:
                newData.append(item)
        
        # Creamos una imagen nueva con los datos limpios para evitar errores de buffer
        f.putdata(newData)
        
        # 4. VOLVER A MODO PALETA (Para GIF)
        # Importante: convert("P") después de putdata
        f_final = f.convert("P", palette=Image.ADAPTIVE, colors=255)
        frames.append(f_final)

    # 5. GUARDAR
    frames[0].save(
        './assets/darksign_transparent2.gif',
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=original_duration,
        loop=0,
        transparency=0,
        disposal=2 
    )

print(f"¡Listo! Recortado a {CROP_SIZE}x{CROP_SIZE} y con transparencia.")