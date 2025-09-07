import os
import geopandas
import pandas as pd
from shapely.geometry import MultiPolygon

cwd = os.path.join(os.getcwd(),'area_info')
folders = [x for x in os.listdir(cwd) if not os.path.isfile(x)]
shp_files = [os.path.join(cwd, x, "TL_SCCO_SIG.shp") for x in folders]

geodf = geopandas.GeoDataFrame()

for file in shp_files:
    temp = geopandas.read_file(file,encoding='cp949')
    geodf = pd.concat([geodf,temp], sort=False).reset_index(drop=True)

geodf.to_file('법정구역_시군구.geojson', driver='GeoJSON')


# threshold_area보다 작은 크기의 도형(구역)들은 제외한 나머지 도형들만 담아서 반환하는 함수
def filter_small_polygons(multi_polygon, threshold_area):
    filtered_polygons = []
    if type(multi_polygon)==MultiPolygon:
        for polygon in list(multi_polygon.geoms):
            if polygon.area >= threshold_area:
                filtered_polygons.append(polygon)
        
        return MultiPolygon(filtered_polygons)
    else:
        return multi_polygon
    

geodf['geometry'] = geodf['geometry'].apply(lambda x: filter_small_polygons(x, threshold_area=7000000))
# threshold를 더 크게 설정할 경우 지워지는 구역이 생깁니다.

geodf['geometry'] = geodf['geometry'].simplify(100)
# simplyfy 함수는 꼬불꼬불한 테두리를 일자로 펴줍니다.

geodf = geodf.set_crs(epsg=5179)
geodf = geodf.to_crs(epsg=4326)
# 좌표계를 바꾸는 것은 섬을 지운 이후에 적용해줍니다.

geodf.to_file('법정구역_시군구.geojson', driver='GeoJSON')