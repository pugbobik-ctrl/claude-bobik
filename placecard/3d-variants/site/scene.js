// Shared scene: table, light, camera views. Used by the viewer page and the screenshot tool.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { bounds } from './fold.js';

export function makeScene(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NoToneMapping;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xd3cfc6);
  const pm = new THREE.PMREMGenerator(renderer);
  scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.12;

  const table = new THREE.Mesh(new THREE.PlaneGeometry(6000, 6000),
    new THREE.MeshLambertMaterial({ color: 0xb9b3a7 }));
  table.rotation.x = -Math.PI / 2;
  table.receiveShadow = true;
  scene.add(table);

  scene.add(new THREE.HemisphereLight(0xffffff, 0xc9c1ae, 1.9));
  const sun = new THREE.DirectionalLight(0xffffff, 1.55);
  sun.position.set(-300, 900, 500);
  sun.castShadow = true;
  sun.shadow.mapSize.set(4096, 4096);
  const sc = sun.shadow.camera;
  sc.left = -500; sc.right = 500; sc.top = 500; sc.bottom = -500; sc.near = 10; sc.far = 3000;
  sun.shadow.bias = -0.0004;
  sun.shadow.normalBias = 0.6;
  scene.add(sun);

  const camera = new THREE.PerspectiveCamera(35, 1, 5, 20000);
  return { renderer, scene, camera, sun, table };
}

// Camera placement for a named view. Seat = the guest's eye from the spec.
export function viewPose(view, object, spec, aspect = 1.4) {
  const narrow = Math.min(1, aspect);            // fit the width too on portrait screens
  const b = bounds(object, true);               // frame the card; props may run out of frame
  const c = b.getCenter(new THREE.Vector3());
  const r = Math.max(60, b.getSize(new THREE.Vector3()).length() / 2);
  const dirs = {
    front: new THREE.Vector3(0, 0.18, 1), side: new THREE.Vector3(1, 0.2, 0.05), top: new THREE.Vector3(0, 1, 0.001),
    orbit: new THREE.Vector3(0.75, 0.62, 1), back: new THREE.Vector3(-0.2, 0.35, -1),
  };
  if (view === 'seat') {
    // the guest's eye, framed on the card (the real view is the same picture, just smaller)
    const eye = new THREE.Vector3(...(spec.eye || [0, 430, 450]));
    const cb = bounds(object, true), cc = cb.getCenter(new THREE.Vector3());
    const cr = Math.max(40, cb.getSize(new THREE.Vector3()).length() / 2);
    const fov = Math.min(75, Math.max(8, 2 * THREE.MathUtils.radToDeg(Math.atan(cr * 1.15 / narrow / eye.distanceTo(cc)))));
    return { pos: eye, target: cc, fov };
  }
  const d = (dirs[view] || dirs.orbit).clone().normalize();
  const fov = 35;
  const dist = r / Math.sin(THREE.MathUtils.degToRad(fov / 2)) * 1.05 / narrow;
  return { pos: c.clone().add(d.multiplyScalar(dist)), target: c, fov };
}
