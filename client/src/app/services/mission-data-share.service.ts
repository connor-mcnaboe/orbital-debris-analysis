import { Injectable } from '@angular/core';
import {ReplaySubject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class MissionDataShareService {

  missionSubject = new ReplaySubject<ThreatReport>();
  $mission = this.missionSubject.asObservable();
  constructor() { }

  update_mission(threatReport: ThreatReport): void {
    this.missionSubject.next(threatReport)
  }
}

export interface ThreatReport {
  total_threat_count: number
  rocket_body_threat_count: number
  debris_threat_count: number
  inactive_sat_threat_count: number
  active_sat_threat_count: number
}
