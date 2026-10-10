import React from 'react';
import {AbsoluteFill, Composition, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const opacity = interpolate(frame, [0, 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const progress = spring({frame, fps, config: {damping: 18}});
  const scale = 0.85 + progress * 0.15;
  return <AbsoluteFill style={{backgroundColor: '#102d30', justifyContent: 'center', alignItems: 'center', color: '#edf9f6', fontFamily: 'sans-serif'}}>
    <div style={{opacity, transform: `scale(${scale})`, textAlign: 'center'}}>
      <div style={{fontSize: 96, fontWeight: 700}}>Codex</div>
      <div style={{fontSize: 40, marginTop: 24}}>Plan → Execute → Verify</div>
    </div>
    <div style={{position: 'absolute', bottom: 80, height: 8, backgroundColor: '#64dfca', width: `${(frame / 149) * 80}%`}} />
  </AbsoluteFill>;
};
export const Root: React.FC = () => <Composition id="CodexIntro" component={Intro} durationInFrames={150} fps={30} width={1280} height={720} />;
